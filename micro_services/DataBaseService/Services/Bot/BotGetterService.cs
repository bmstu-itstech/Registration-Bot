using Grpc.Core;
using System.Net;
using DataBaseService.DataBase;
namespace DataBaseService.Services.bot
{
    public class BotGetterService : BotGetter.BotGetterBase
    {
        private readonly ILogger<BotGetterService> _logger;

        public BotGetterService(ILogger<BotGetterService> logger)
        {
            _logger = logger;
        }

        public override Task<BotSurvey> GetBotById(GetBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Get Bot by id Request");

            BotSurvey botSurvey = null;

            //
            // METHODS
            //

            return Task.FromResult(new BotSurvey
            {
                BotId = 1,
                Title = "BCG BOT"
            });
        }
    }
}
