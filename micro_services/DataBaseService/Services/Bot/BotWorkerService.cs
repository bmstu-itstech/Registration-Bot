using Grpc.Core;

using DataBaseService.Protos;
using DataBaseService.Backend.Types;
using MyJournal = DataBaseService.Backend.Types.MyJournal;
using System.Linq;
using DataBaseService.backend.Types;

namespace DataBaseService.Services.Bot
{
    public class BotWorkerService : BotWorker.BotWorkerBase
    {

        private readonly ILogger<BotWorkerService> _logger;

        public BotWorkerService(ILogger<BotWorkerService> logger)
        {
            _logger = logger;
        }
        public override Task<CreateBotResponse> CreateBot(CreateBotRequest request, ServerCallContext context)
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

                MyBot.UpdateBotGoogleToken(request.SheetsToken, bot_id, request.FromUser);
                MyBot.UpdateBotTgToken(request.TgToken, bot_id, request.FromUser);
                MyBot.UpdateStartMessage(request.StartMessage, bot_id, request.FromUser);

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

        public override Task<BaseResponse> SetAnswers(SetAnswersRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Set new Answer Request {request.TgChatId} ");

            string state = "OK";
            int code = 200;

            try
            {

                List<MyAnswer> answers = request.Answers.Select(answer => MyAnswer.ConvertFromRPC(answer)).ToList();

                MyBot.SetAnswers(request.BotId, request.TgChatId, answers);
            }
            catch (Exception ex)
            {
                state = ex.Message;
                code = 401;
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
