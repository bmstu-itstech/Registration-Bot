using Grpc.Core;
using DataBaseService.DataBase;
using DataBaseService.Protos;
using DataBaseService.Backend.Types;
using Journal = DataBaseService.Backend.Types.Journal;
using System.Linq;

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

            Journal my_journal = new Journal()
            {
                Modules = request.Journal.Modules.ToDictionary(m => m.Key, m => new Backend.Types.Module 
                { 
                    Answers = m.Value.Answers.ToList(),
                    Question = m.Value.Question,

                })
            };

            DataBase.BotSurvey.CreateNewBotSurvey(request.FromUser, my_journal).Wait();


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

            //
            // METHODS
            //

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }
    }
}
