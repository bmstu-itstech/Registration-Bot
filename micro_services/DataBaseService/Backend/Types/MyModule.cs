using DataBaseService.Backend.Config;
using DataBaseService.Backend.Exeptions;
using DataBaseService.Models;
using DataBaseService.Protos;
using Npgsql;

namespace DataBaseService.Backend.Types
{
    public class MyModule
    {
        public int Id { get; set; }
        public string Question { get; set; }
        public string AnswerType { get; set; }
        public string Title { get; set; }
        public string QuestionType { get; set; }
        public List<MyButton> buttons { get; set; }
        public int NextQuestionId { get; set; }

        public static MyModule ConvertFromRPC(Module _module)
        {
            return new MyModule
            {
                Id = _module.Id,
                Question = _module.Question,
                Title = _module.Title,
                AnswerType = _module.AnswerType,
                QuestionType = _module.QuestionType,
                buttons = _module.Buttons.Select(button => MyButton.ConvertFromRPC(button)).ToList(),
                NextQuestionId = _module.NextQuestionId
            };

        }
        public static Module ConvertToRPC(MyModule module)
        {
            Module _module = new Module();

            _module.Id = module.Id;
            _module.Question = module.Question;
            _module.AnswerType = module.AnswerType;
            _module.QuestionType = module.QuestionType;
            _module.NextQuestionId = module.NextQuestionId;
            _module.Title = module.Title;

            if (module.buttons != null && module.buttons.Count > 0)
                _module.Buttons.AddRange(module.buttons.Select
                    (button => MyButton.ConvertToRPC(button)).ToList());

            return _module;
        }

        public static Task<MyModule> GetMoudleById(int data_base_id, int module_id)
        {
            return Task.Run(async () =>
            {

                using (var conn = new NpgsqlConnection(new ConfigManager().GetBotConnetion(data_base_id)))
                {
                    await conn.OpenAsync();
                    try
                    {
                        string select = $"SELECT * FROM questions WHERE id={module_id} LIMIT 1--";
                        string select_question_buttons = $"SELECT * FROM buttons WHERE question_id={module_id}--";

                        MyModule module = new MyModule();
                        List<MyButton> buttons = new List<MyButton>();


                        using (var command = new NpgsqlCommand(select_question_buttons, conn))
                        {
                            using (var reader = await command.ExecuteReaderAsync())
                            {
                                while (await reader.ReadAsync())
                                {
                                    buttons.Add(new MyButton()
                                    {
                                        Id = reader.GetInt32(0),
                                        QuestionId = reader.GetInt32(1),
                                        NextQuestionId = reader.GetInt32(2),
                                        Answer_text = reader.GetString(3)
                                    });
                                }
                            }
                        }

                        using (var command = new NpgsqlCommand(select, conn))
                        {

                            using (var reader = await command.ExecuteReaderAsync())
                            {
                                while (await reader.ReadAsync())
                                {
                                    module.Id = reader.GetInt32(0);
                                    module.Question = reader.GetString(1);
                                    module.QuestionType = reader.GetString(2);
                                    module.AnswerType = reader.GetString(4);
                                    module.Title = reader.GetString(5);

                                    if (buttons.Count > 0)
                                        module.buttons = buttons;

                                    try
                                    {
                                        module.NextQuestionId = reader.GetInt32(3);
                                    }
                                    catch (Exception)
                                    {
                                        module.NextQuestionId = 0;
                                    }
                                }
                            }
                        }

                        return module;
                    }
                    catch (Exception ex)
                    {
                        throw new DataBaseError("Error in GetMoudleById ()\n" + ex.Message);
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
