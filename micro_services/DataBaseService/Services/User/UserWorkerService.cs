using DataBaseService.Protos;
using DataBaseService.Services.Bot;
using Grpc.Core;

namespace DataBaseService.Services.User
{
    public class UserWorkerService : UserWorker.UserWorkerBase
    {

        private readonly ILogger<UserWorkerService> _logger;

        public UserWorkerService(ILogger<UserWorkerService> logger)
        {
            _logger = logger;
        }

        public override Task<BaseResponse> EndReg(EndRegRequest request, ServerCallContext context)
        {
            _logger.LogInformation("End Rigistatrion request");

            string state = "OK";
            int code = 200;

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            }) ;
        }

        public override Task<BaseResponse> RegNewUser(RegUserRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Reg new user in bot {request.BotId}");

            string state = "OK";
            int code = 200;

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }
    }
}
