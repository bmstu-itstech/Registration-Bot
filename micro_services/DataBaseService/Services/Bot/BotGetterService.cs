using Grpc.Core;
using System.Net;
using DataBaseService.DataBase;
using DataBaseService.Protos;

namespace DataBaseService.Services.bot
{
    public class BotGetterService : BotGetter.BotGetterBase
    {
        private readonly ILogger<BotGetterService> _logger;

        public BotGetterService(ILogger<BotGetterService> logger)
        {
            _logger = logger;
        }

        public override Task<Protos.BotResponse> GetBotById(GetBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Get Bot by id Request");

            Protos.BotResponse botSurvey = null;

            //
            // METHODS
            //

            return Task.FromResult(new Protos.BotResponse
            {
              
            });
        }
    }
}
