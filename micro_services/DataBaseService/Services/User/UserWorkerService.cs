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

        public override Task<UserResponse> GetUser(GetUserRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Get user {request.UserId} Request");


            return base.GetUser(request, context);
        }

        public override Task<GetUserBotsListResponse> GetUserBotsList(GetUserBotsListRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Get user {request.UserId} bots Request");


            return base.GetUserBotsList(request, context);
        }

        public override Task<BaseResponse> RegNewUser(Protos.User request, ServerCallContext context)
        {
            _logger.LogInformation($"reg new user Request");

            string state = "OK";
            int code = 200;

            // 
            // METHODS
            //

            return Task.FromResult(new BaseResponse
            {
                State = state,
                Code = code,
            });
        }
    }
}
