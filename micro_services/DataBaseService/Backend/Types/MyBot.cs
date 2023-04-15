using DataBaseService.Backend.Config;
using DataBaseService.Models;
using Npgsql;

using DataBaseService.Backend.Types;
using DataBaseService.Backend.Exeptions;

namespace DataBaseService.backend.Types
{
    public class MyBot
    {
        public int Id { get; set; }
        public string tg_token { get; set; }
        public string google_token { get; set; }
        public int owner { get; set; }
        public int bot_survey_id { get; set; }


        public static Task CreateNewBotSurvey(int user_id, MyJournal journal)
        {
            return Task.Run(async () =>
            {
                Dictionary<string, string> colums = new Dictionary<string, string>();

                foreach (var module in journal.Modules)
                {
                    colums.Add(key: module.Value.Title, value: module.Value.Type);
                }


                int next_bot_id = GenerateNewBotId().Result;

                CreateBotSurveyDataBase(next_bot_id).Wait();

                await CreateBotSurveyAnswerTable(next_bot_id, colums);
                await CreateBotSurveyAdminTable(next_bot_id);
                await CreateBotSurveyButtons(next_bot_id);
                await CreateBotSurveyQuestionsTable(next_bot_id);



                await FillBotSurveyQuestionTable(next_bot_id, journal);

                try
                {
                    await AddNewBot(next_bot_id, user_id);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex);
                }

            });

        }
        public static Task DeleteBotSurvey(int user_id, int bot_id)
        {

            return Task.Run(async () =>
            {

                await DropBotSurveyAnswerTable(bot_id);
                await DroBotSurveyAdminTable(bot_id);
                await DropBotSurveyButtonsTable(bot_id);
                await DropBotSurveyQuestionTable(bot_id);

                await DropBotSurveyDataBase(bot_id);

                await RemoveBot(bot_id, user_id);

                
            });
        }

        public static Task UpdateBotTgToken(string token, int bot_survey_id, int owner)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {

                    var bot = db.Bots.Where(bot => bot.Owner == owner).Where(bot => bot.BotId == bot_survey_id).First();

                    bot.TgToken = token;


                    await db.SaveChangesAsync();

                }
            });
        }
        public static Task UpdateBotGoogleToken(string token, int bot_survey_id, int owner)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {

                    var bot = db.Bots.Where(bot => bot.Owner == owner).Where(bot => bot.BotId == bot_survey_id).First();

                    bot.GoogleToken = token;


                    await db.SaveChangesAsync();

                }

            });
        }
        public static Task<MyBot> GetBot(int bot_survey_id, int owner)
        {
            return Task.Run(() =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {

                    var bot = db.Bots.Where(bot => bot.Owner == owner).Where(bot => bot.BotId == bot_survey_id).First();

                    return new MyBot
                    {
                        Id = bot.Id,
                        tg_token = bot.TgToken,
                        google_token = bot.GoogleToken,
                        owner = bot.Owner,
                        bot_survey_id = bot.BotId
                    };

                }
            });
        }

        private static async Task<int> GenerateNewBotId()
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string get_next_id = "SELECT nextval('bot_id_sequence');--";

                using (var command = new NpgsqlCommand(get_next_id, conn))
                {
                    using (var reader = await command.ExecuteReaderAsync())
                    {

                        await reader.ReadAsync();

                        return (int)reader.GetInt64(0);
                    }
                }


            }
        }

        private static Task CreateBotSurveyDataBase(int data_base_id)
        {
            return Task.Run(async () =>
            {

                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    string create_database = $"CREATE DATABASE BOT_{data_base_id} OWNER postgres--";

                    try
                    {
                        using (var command = new NpgsqlCommand(create_database, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while creating new bot Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }

                }

            });
        }
        private static Task CreateBotSurveyQuestionsTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string create_table = $"CREATE TABLE questions " +
                    $"(" +
                    $"ID SERIAL PRIMARY KEY," +
                    $"next_ids CHARACTER VARYING(255)," +
                    $"question_text CHARACTER VARYING(255) NOT NULL" +
                    $")--";

                    using (var command = new NpgsqlCommand(create_table, conn))
                    {
                        await command.ExecuteNonQueryAsync();
                    }
                }



            });
        }
        private static Task CreateBotSurveyAnswerTable(int data_base_id, Dictionary<string, string> colums)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string create_table = $"CREATE TABLE answers" +
                    "(" +
                    $"user_chat_id BIGINT PRIMARY KEY," +
                    $"code INTEGER" +
                    ")--";

                    try
                    {
                        using (var command = new NpgsqlCommand(create_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }

                        foreach (var col in colums)
                        {
                            string alter_table = $"ALTER TABLE answers ADD COLUMN {col.Key} {col.Value} --";

                            using (var command = new NpgsqlCommand(alter_table, conn))
                            {
                                await command.ExecuteNonQueryAsync();
                            }

                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while creating new bot Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
        }
        private static Task CreateBotSurveyButtons(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string create_table = $"CREATE TABLE buttons" +
                    "(" +
                    $"id SERIAL PRIMARY KEY," +
                    $"question_id INTEGER," +
                    $"next_question_id INTEGER," +
                    $"answer_text TEXT," +
                    $"FOREIGN KEY (question_id) REFERENCES questions(id)" +
                    ")--";

                    try
                    {
                        using (var command = new NpgsqlCommand(create_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }


                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while creating new bot Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });

        }
        private static Task CreateBotSurveyAdminTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string create_table = $"CREATE TABLE admins " +
                    "(" +
                    $"admin_tg BIGINT PRIMARY KEY," +
                    $"curr_cmd CHARACTER VARYING(255)," +
                    $"is_main_admin BOOLEAN" +
                    ")--";

                    try
                    {
                        using (var command = new NpgsqlCommand(create_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {

                        throw new DataBaseError($"Erorr while creating new bot Survey table\n{ex.Message}");
                    }


                }
            });
        }

        private static Task DropBotSurveyDataBase(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    string drop_table = $"DROP DATABASE BOT_{data_base_id}--";

                    try
                    {
                        using (var command = new NpgsqlCommand(drop_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while droppin bot Survey database\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
           
        }
        private static Task DropBotSurveyAnswerTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string drop_table = $"DROP TABLE answers--";

                    try
                    {
                        using (var command = new NpgsqlCommand(drop_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while droppin answers Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
        }
        private static Task DroBotSurveyAdminTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string drop_table = $"DROP TABLE admins--";

                    try
                    {
                        using (var command = new NpgsqlCommand(drop_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while droppin admins Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
        }
        private static Task DropBotSurveyButtonsTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string drop_table = $"DROP TABLE buttons--";

                    try
                    {
                        using (var command = new NpgsqlCommand(drop_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while droppin admins Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
        }
        private static Task DropBotSurveyQuestionTable(int data_base_id)
        {
            return Task.Run(async () =>
            {
                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();

                    string drop_table = $"DROP TABLE questions--";

                    try
                    {
                        using (var command = new NpgsqlCommand(drop_table, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError($"Erorr while droppin admins Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                    }
                }
            });
        }

        private static Task<string> generate_insert_into_bot_survey(int bot_id, int module_id, MyModule module)
        {
            return Task.Run(() =>
            {
                string next_ids = string.Empty;
                string answers = string.Empty;

                foreach (var next_id in module.Next_ids)
                    next_ids += next_id.ToString() + "\\";

                foreach (var answer in module.Answers)
                    answers += answer.ToString() + '\\';

                if (next_ids != string.Empty)
                    next_ids = next_ids.Remove(next_ids.Length - 1, 1);

                if (answers != string.Empty)
                    answers = answers.Remove(answers.Length - 1, 1);


                string insert = $"INSERT INTO bot_{bot_id} (module_id,next_ids,question_text,answers) VALUES" +
                    $"(" +
                    $"{module_id}," +
                    $"'{next_ids}'," +
                    $"'{module.Question}'," +
                    $"'{answers}')" +
                    $"--";



                return insert;
            });
        }

        private static async Task FillBotSurveyQuestionTable(int bot_id, MyJournal journal)
        {

            foreach (var modul in journal.Modules)
            {

                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    try
                    {
                        using (var command = new NpgsqlCommand(generate_insert_into_bot_survey(bot_id, modul.Key, modul.Value).Result, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex);

                    }

                }
            }
        }


        private static Task AddNewBot(int bot_survey_id, int owner)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {
                    var bot = new Bot
                    {
                        BotId = bot_survey_id,
                        Owner = owner,
                        TgToken = "",
                        GoogleToken = ""

                    };

                    await db.Bots.AddAsync(bot);
                    db.Users.Where(user => user.Id == owner).First().Bots.Add(bot);

                    await db.SaveChangesAsync();

                }
            });
        }
        private static Task RemoveBot(int bot_survey_id, int owner)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {


                    var bot = db.Bots.Where(bot => bot.Owner == owner).Where(bot => bot.BotId == bot_survey_id).First();

                    db.Bots.Remove(bot);

                    await db.SaveChangesAsync();

                }
            });

        }
    }
}
