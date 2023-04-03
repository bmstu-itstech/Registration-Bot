using Grpc.Core;
using DataBaseService.DataBase;

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

            var modules = request.Modules.ToDictionary(m => m.Key, m => m.Value);


            DataBase.BotSurvey.CreateNewBotSurvey(request.FromUser,modules).Wait();


            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            }) ;
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
