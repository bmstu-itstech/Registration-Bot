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
        public override Task<BaseResponse> CreateBot(CreateBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Create new Bot Survey Request");

            string state = "OK";
            int code = 200;

            var journal = request.Journal;

            MyJournal my_journal = new MyJournal()
            {
                Modules = request.Journal.Modules.ToDictionary(m => m.Key, m => new MyModule
                {
                    Answers = m.Value.Answers.ToList(),
                    Question = m.Value.Question,
                    Title = m.Value.Title,
                    Type = m.Value.Type,
                    Next_ids = m.Value.NextIds.ToList(),
                })
            };

            //main code 
            try
            {


                var response = MyBot.CreateNewBotSurvey(request.FromUser, my_journal);

                response.Wait();

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


            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
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
