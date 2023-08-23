using DataBaseService.Backend.Config;
using DataBaseService.Models;
using Npgsql;

using DataBaseService.Backend.Types;
using DataBaseService.Backend.Exeptions;
using DataBaseService.Protos;
using System.Text;

namespace DataBaseService.backend.Types
{
    public class MyBot
    {
        public int Id { get; set; }
        public string tg_token { get; set; }
        public string google_token { get; set; }
        public int owner { get; set; }
        public int bot_survey_id { get; set; }


        public static Task<int> CreateNewBotSurvey(int user_id, MyJournal journal)
        {
            return Task.Run(async () =>
            {
                Dictionary<string, string> colums = new Dictionary<string, string>();

                foreach (var module in journal.Modules)
                {
                    colums.Add(key: module.Value.Title, value: module.Value.AnswerType);
                }


                try
                {


                    int next_bot_id = GenerateNewBotId().Result;


                    CreateBotSurveyDataBase(next_bot_id).Wait();


                    await CreateBotSurveyAnswerTable(next_bot_id, colums);
                    await CreateBotSurveyAdminTable(next_bot_id);
                    await CreateBotSurveyQuestionsTable(next_bot_id);

                    await CreateBotSurveyButtons(next_bot_id);


                    await FillBotSurveyQuestionTable(next_bot_id, journal);

                    foreach (var module in journal.Modules)
                    {
                        module.Value.buttons = module.Value.buttons.Select(bnt => new MyButton
                        {
                            Answer = bnt.Answer,
                            NextId = bnt.NextId,
                            Question_id = module.Key
                        }).ToList();

                        await FillBotSurveyButtonsTable(next_bot_id, module.Value.buttons);

                    }

                    await AddNewBot(next_bot_id, user_id);


                    return next_bot_id;

                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex);

                    throw;
                }
            });

        }
        public static Task DeleteBotSurvey(int user_id, int bot_id)
        {

            return Task.Run(async () =>
            {

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
            try
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
            catch (Exception ex)
            {
                Console.WriteLine(ex);
                throw;
            }

        }

        private static Task CreateBotSurveyDataBase(int data_base_id)
        {
            return Task.Run(async () =>
            {

                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    string create_database = $"CREATE DATABASE bot_{data_base_id} OWNER postgres--";

                    try
                    {
                        using (var command = new NpgsqlCommand(create_database, conn))
                        {
                            await command.ExecuteNonQueryAsync();
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex);
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
                    $"id INTEGER PRIMARY KEY," +
                    $"question_text TEXT NOT NULL," +
                    $"next_id INTEGER," +
                    $"answer_type CHARACTER VARYING(255)," +
                    $"collum_title CHARACTER VARYING(255) " +
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
                try
                {
                    using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                    {
                        await conn.OpenAsync();

                        string create_table = $"CREATE TABLE answers" +
                        "(" +
                        $"user_chat_id BIGINT PRIMARY KEY," +
                        $"code SERIAL" +
                        ")--";

                        try
                        {
                            using (var command = new NpgsqlCommand(create_table, conn))
                            {
                                await command.ExecuteNonQueryAsync();
                            }

                            foreach (var col in colums)
                            {
                                // Title // Data_Type 
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
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex);
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
                    $"next_id INTEGER," +
                    $"answer TEXT," +
                    $"question_id INTEGER," +
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

        private static Task<string> generate_insert_into_bot_survey(int module_id, MyModule module)
        {
            return Task.Run(() =>
            {
                return Task.Run(() =>
                {
                    string insert = string.Empty;

                    if (module.NextId == 0)
                    {
                        insert = $"INSERT INTO questions (id,question_text,answer_type,collum_title) VALUES(" +
                          $"{module_id}," +
                          $"'{module.Question}'," +
                          $"'{module.AnswerType}'," +
                          $"'{module.Title}'" +
                          $")--";
                    }
                    else
                    {
                        insert = $"INSERT INTO questions (id,question_text,answer_type,collum_title,next_id) VALUES(" +
                                 $"{module_id}," +
                                 $"'{module.Question}'," +
                                 $"'{module.AnswerType}'," +
                                 $"'{module.Title}'," +
                                 $"{module.NextId}" +
                                 $")--";
                    }

                    return insert;
                });
            });
        }
        private static Task<string> generate_insert_into_bot_survey_buttons(MyButton button)
        {
            return Task.Run(() =>
            {
                string insert = $"INSERT  INTO buttons (next_id,answer,question_id) VALUES(" +
                $"{button.NextId}," +
                $"'{button.Answer}'," +
                $"{button.Question_id}" +
                $")--";

                return insert;
            });
        }

        private static Task FillBotSurveyQuestionTable(int data_base_id, MyJournal journal)
        {
            return Task.Run(async () =>
            {
                foreach (var modul in journal.Modules)
                {

                    using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                    {
                        await conn.OpenAsync();

                        try
                        {
                            using (var command = new NpgsqlCommand(generate_insert_into_bot_survey(modul.Key, modul.Value).Result, conn))
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
            });

        }
        private static Task FillBotSurveyButtonsTable(int data_base_id, List<MyButton> buttons)
        {
            return Task.Run(async () =>
            {
                foreach (var button in buttons)
                {
                    using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                    {
                        await conn.OpenAsync();

                        try
                        {
                            using (var command = new NpgsqlCommand(generate_insert_into_bot_survey_buttons(button).Result, conn))
                            {
                                await command.ExecuteNonQueryAsync();
                            }
                        }
                        catch (Exception ex)
                        {

                        }

                    }
                }
            });
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


        public static Task SetAnswers(int data_base_id, long chatId, List<MyAnswer> answers)
        {
            return Task.Run(async () =>
            {


                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();
                    Console.WriteLine(1234);
                    try
                    {
                        try
                        {
                            string create_new_answer = $"INSERT INTO answers (user_chat_id) VALUES({chatId})";

                            using (var command = new NpgsqlCommand(create_new_answer, conn))
                            {
                                await command.ExecuteNonQueryAsync();
                            }

                            foreach (var answer in answers)
                            {
                                var _module = MyModule.GetMoudleById(data_base_id, answer.Module_Id).Result;

                                string collum_type = _module.AnswerType;
                                string collum_title = _module.Title;

                                object _answer = null;
                                string update = string.Empty;


                                if (collum_type == "BOOLEAN")
                                    _answer = Convert.ToBoolean(answer.Answer);
                                else if (collum_type == "INTEGER")
                                    _answer = Convert.ToInt32(answer.Answer);

                                if (collum_type == "TEXT")
                                    update = $"UPDATE answers SET {collum_title} = '{answer.Answer}' WHERE user_chat_id = {chatId}--";
                                else
                                    update = $"UPDATE answers SET {collum_title} = {_answer} WHERE user_chat_id = {chatId}--";


                                Console.WriteLine(update);
                                using (var command = new NpgsqlCommand(update, conn))
                                {
                                    await command.ExecuteNonQueryAsync();
                                }
                            }
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine(ex);

                            throw;
                        }

                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError("Erorr in SetAnswers\n" + ex);
                    }
                    finally
                    {
                        await conn.CloseAsync();
                    }
                }

            });
        }

    }
}
