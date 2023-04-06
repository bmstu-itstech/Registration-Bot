using DataBaseService.Backend.Config;
using DataBaseService.Backend.Types;
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

            string state = "OK";
            int code = 200;




            return base.GetUser(request, context);
        }

        public override Task<GetUserBotsListResponse> GetUserBotsList(GetUserBotsListRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Get user {request.UserId} bots Request");

            string state = "OK";
            int code = 200;
            
            List<BotResponse> response_bots = new List<BotResponse>();
            var user_bots = OrgUser.GetUserBots(request.UserId).Result;

            var response = new GetUserBotsListResponse();

            if (user_bots == null)
            {
                state = "Erorr while geting user bots";
                code = 401;

                foreach(var bot in user_bots)
                {
                    response_bots.Add(new BotResponse
                    { 
                        Id = bot.Id,
                        BotSurveyId = bot.bot_survey_id,
                        TgToken = bot.tg_token,
                        GoogleToken = bot.google_token,
                        Owner = bot.owner,

                    });
                }
            }


            response.State = state;
            response.Code = code;
            response.Bots.AddRange(response_bots);

            return Task.FromResult(response);
        }

        public override  Task<BaseResponse> RegNewUser(Protos.User request, ServerCallContext context)
        {
            _logger.LogInformation($"reg new user Request");

            string state = "OK";
            int code = 200;

        
            var response = OrgUser.Registration(request);
            response.Wait();

            if(response.IsFaulted)
            {
                state = "Error while registar new user";
                code = 401;
            }


            return Task.FromResult(new BaseResponse
            {
                State = state,
                Code = code,
            });
        }
    }
}
