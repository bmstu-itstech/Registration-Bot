using DataBaseService.backend.Types;
using DataBaseService.Backend.Config;
using DataBaseService.Backend.Exeptions;
using DataBaseService.Backend.Types;

using Npgsql;
using System.ComponentModel.DataAnnotations;

namespace DataBaseService.DataBase
{
    public class BotSurvey
    {
        public static Task CreateNewBotSurvey(int user_id, MyJournal journal)
        {
            return Task.Run(async () =>
            {
                Dictionary<string, string> colums = new Dictionary<string, string>();

                foreach (var module in journal.Modules)
                {
                    colums.Add(key: module.Value.Title, value: module.Value.Type);
                }

                int bot_id = (int)CreateBotSurveyTable().Result;

                await CreateBotSurveyAnswerTable(bot_id, colums);
                await CreateBotSurveyAdminTable(bot_id);

      

                await FillBotSurveyTable(bot_id, journal);

                try
                {
                    await MyBot.AddNewBot(bot_id, user_id);
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
                await DropBotSurveyTable(bot_id);
                await DropBotSurveyAnswerTable(bot_id);
                await DroBotSurveyAdminTable(bot_id);
            });
        }

        private static async Task<long> CreateBotSurveyTable()
        {
            return await Task.Run(async () =>
            {

                long next_bot_id = -1;

                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    string get_next_id = "SELECT nextval('bot_id_sequence');--";

                    using (var command = new NpgsqlCommand(get_next_id, conn))
                    {
                        using (var reader = await command.ExecuteReaderAsync())
                        {
                            while (await reader.ReadAsync())
                            {
                                next_bot_id = reader.GetInt64(0);
                            }

                        }
                    }

                    if (next_bot_id < 0)
                    {
                        throw new DataBaseError("Erorr while creating new bot Survey table\n next_bot_id less than zero!");
                    }


                    string create_table = $"CREATE TABLE bot_{next_bot_id} " +
                    $"(" +
                    $"module_id INT PRIMARY KEY," +
                    $"next_ids CHARACTER VARYING(255)," +
                    $"question_text CHARACTER VARYING(255) NOT NULL," +
                    $"answers CHARACTER VARYING(255)" +
                    $")--";


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

                return next_bot_id;
            });
        }
        private static async Task CreateBotSurveyAnswerTable(int bot_id, Dictionary<string, string> colums)
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string create_table = $"CREATE TABLE bot_{bot_id}_answers " +
                "(" +
                $"user_id BIGINT PRIMARY KEY," +
                $"prev_id INT," +
                $"now_id INT" +
                ")--";

                try
                {
                    using (var command = new NpgsqlCommand(create_table, conn))
                    {
                        await command.ExecuteNonQueryAsync();
                    }

                    foreach (var col in colums)
                    {
                        string alter_table = $"ALTER TABLE bot_{bot_id}_answers ADD COLUMN {col.Key} {col.Value} --";

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
        private static async Task CreateBotSurveyAdminTable(int bot_id)
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string create_table = $"CREATE TABLE bot_{bot_id}_admins " +
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
        }

        private static async Task DropBotSurveyTable(int bot_id)
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string drop_table = $"DROP TABLE bot_{bot_id}--";

                try
                {
                    using (var command = new NpgsqlCommand(drop_table, conn))
                    {
                        await command.ExecuteNonQueryAsync();
                    }
                }
                catch (Exception ex)
                {
                    throw new DataBaseError($"Erorr while droppin bot{bot_id} Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                }
            }
        }
        private static async Task DropBotSurveyAnswerTable(int bot_id)
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string drop_table = $"DROP TABLE bot_{bot_id}_answers--";

                try
                {
                    using (var command = new NpgsqlCommand(drop_table, conn))
                    {
                        await command.ExecuteNonQueryAsync();
                    }
                }
                catch (Exception ex)
                {
                    throw new DataBaseError($"Erorr while droppin bot_{bot_id}_answers Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                }
            }

        }
        private static async Task DroBotSurveyAdminTable(int bot_id)
        {
            using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
            {
                await conn.OpenAsync();

                string drop_table = $"DROP TABLE bot_{bot_id}_admins--";

                try
                {
                    using (var command = new NpgsqlCommand(drop_table, conn))
                    {
                        await command.ExecuteNonQueryAsync();
                    }
                }
                catch (Exception ex)
                {
                    throw new DataBaseError($"Erorr while droppin bot_{bot_id}_admins Survey table\n {ex.Message}\n\n{ex.StackTrace}");

                }
            }

        }

        private static Task<string> generate_insert_into_bot_survey(int bot_id, int module_id, Module module)
        {
            return Task.Run(() =>
            {
                string next_ids = "";
                string answers = "";

                foreach (var next_id in module.Next_ids)
                    next_ids += next_id.ToString() + "\\";

                foreach (var answer in module.Answers)
                    answers += answer.ToString() + '\\' ;

                next_ids = next_ids.Remove(next_ids.Length - 1, 1);
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

        private static async Task FillBotSurveyTable(int bot_id, MyJournal journal)
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
    }
}
