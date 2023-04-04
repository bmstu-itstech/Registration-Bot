using DataBaseService.Backend.Config;
using DataBaseService.Backend.Exeptions;
using DataBaseService.Backend.Types;

using Npgsql;

namespace DataBaseService.DataBase
{
    public class BotSurvey
    {
        public static Task CreateNewBotSurvey(int user_id, Journal journal)
        {
            return Task.Run(async () =>
            {
                Dictionary<string, string> colums = new Dictionary<string, string>();

                foreach (var module in journal.Modules)
                {
                    colums.Add(key: module.Value.Title, value: module.Value.Type);
                }

                int bot_id = CreateBotSurveyTable().Result;

                await CreateBotSurveyAnswerTable(bot_id, colums);
                await CreateBotSurveyAdminTable(bot_id);

            });

        }
        private static async Task<int> CreateBotSurveyTable()
        {
            return await Task.Run(async () =>
            {

                int next_bot_id = -1;

                using (var conn = new NpgsqlConnection(new ConfigManager().GetConnetion()))
                {
                    await conn.OpenAsync();

                    string get_next_id = "SELECT nextval FROM bot_id_sequence--";

                    using (var command = new NpgsqlCommand(get_next_id, conn))
                    {
                        using (var reader = await command.ExecuteReaderAsync())
                        {
                            next_bot_id = reader.GetInt32(0);
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


        private static async Task FillBotSurveyTable(int bot_id,Journal journal)
        {

        }
    }
}
