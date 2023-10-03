using Grpc.Core;

using DataBaseService.Protos;
using DataBaseService.Backend.Types;
using MyJournal = DataBaseService.Backend.Types.MyJournal;
using System.Linq;
using DataBaseService.backend.Types;
using DataBaseService.Clients;

namespace DataBaseService.Services.Bot
{
    public class BotWorkerService : BotWorker.BotWorkerBase
    {

        private readonly ILogger<BotWorkerService> _logger;

        public BotWorkerService(ILogger<BotWorkerService> logger)
        {
            _logger = logger;
        }
        public override  Task<CreateBotResponse> CreateBot(CreateBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Create new Bot Survey Request");

            string state = "OK";
            int code = 200;
            int bot_id = 0;

            MyJournal my_journal = MyJournal.ConvertFromRPC(request.Journal);

            //main code 
            try
            {

                var response = MyBot.CreateNewBotSurvey(request.FromUser, my_journal);

                response.Wait();
                bot_id = response.Result;

                Dictionary<string, string> colums = new Dictionary<string, string>();

                foreach (var module in my_journal.Modules)
                {
                    colums.Add(key: module.Value.Title, value: module.Value.AnswerType);
                }



                MyBot.UpdateBotGoogleToken(request.SheetsToken, bot_id, request.FromUser).Wait();
                MyBot.UpdateBotTgToken(request.TgToken, bot_id, request.FromUser).Wait();
                MyBot.UpdateStartMessage(request.StartMessage, bot_id, request.FromUser).Wait();
                MyBot.UpdateEndMessage(request.EndMessage, bot_id, request.FromUser).Wait();


                //Вызвать создание листа экселя 

                var header = new List<string>()
                {
                    "Код"
                };

                var journal = my_journal.Modules.OrderBy(module => module.Key);

                foreach (var module in journal)
                {
                    Console.WriteLine(module.Value.Title);
                    header.Add(module.Value.Title);
                }

               

                
                header.Add("Линк телеграм");
                header.Add("Дата регистрации");


                SheetsClient.AddBaseSheet(bot_id, request.FromUser, header).Wait();

                if (response.IsFaulted)
                {
                    state = "Erorr while Creating new Bot Survey";
                    code = 401;
                }

            }
            catch (Exception ex)
            {
                state = $"Erorr while Creating new Bot Survey\n{ex.Message}";
                code = 401;
            }


            return Task.FromResult(new CreateBotResponse()
            {
                State = state,
                Code = code,
                BotId = bot_id
            });
        }

        public override Task<BaseResponse> DeleteBot(DeleteBotRequest request, ServerCallContext context)
        {

            _logger.LogInformation("Delete new Bot Request");

            string state = "OK";
            int code = 200;

            //main code 
            try
            {


                var response = MyBot.DeleteBotSurvey(request.FromUser, request.BotId);

                response.Wait();

                if (response.IsFaulted)
                {
                    state = "Erorr while Deleting Bot Survey";
                    code = 401;
                }

            }
            catch (Exception ex)
            {
                state = $"Erorr while Deleting Bot Survey\n{ex.Message}";
                code = 401;
            }

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }

        public override  Task<BaseResponse> SetAnswers(SetAnswersRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Set new Answer Request {request.TgChatId} ");

            string state = "OK";
            int code = 200;

            try
            {

                List<MyAnswer> answers = request.Answers.Select(answer => MyAnswer.ConvertFromRPC(answer)).ToList();
                Dictionary<int, string> all_answers = new Dictionary<int, string>();
               
                for(int i = 1; i <=  MyBot.GetQuestionCount(request.BotId).Result; i++)
                {
                    all_answers[i] = "";
                }
                foreach (var answer in answers)
                {
                    all_answers[answer.Module_Id] = answer.Answer;
                }
                int user_code =  MyBot.SetAnswers(request.BotId, request.TgChatId,request.TelegramLink, answers).Result;

                code = user_code;

                // Вызвать метод таблц
                SheetsClient.InputUser(request.BotId, user_code, request.TelegramLink, all_answers);
            }
            catch (Exception ex)
            {
                
                state = ex.Message;
                code = 0;
            }

            return Task.FromResult(new BaseResponse
            {
                State = state,
                Code = code
            });
        }

        public override Task<BaseResponse> UpdateBotGoogleToken(UpdateBotGoogleTokenRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Update Bot {request.BotId} Google Token Request");

            string state = "OK";
            int code = 200;

            var response = MyBot.UpdateBotGoogleToken(request.Token, request.BotId, request.Owner);

            if (response.IsFaulted)
            {
                state = "Error while updating google token";
                code = 401;
            }


            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }

        public override Task<BaseResponse> UpdateBotTgToken(UpdateBotTgTokenRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Update Bot {request.BotId} Google Token Request");

            string state = "OK";
            int code = 200;

            var response = MyBot.UpdateBotTgToken(request.Token, request.BotId, request.Owner);


            if (response.IsFaulted)
            {
                state = "Error while updating google token";
                code = 401;
            }

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }
    }
}
