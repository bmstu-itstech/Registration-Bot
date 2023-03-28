using Grpc.Core;
using System.Net;

namespace DataBaseService.Services
{
    public class BotGetterService : BotGetter.BotGetterBase
    {
        private readonly ILogger<BotGetterService> _logger;

        public BotGetterService(ILogger<BotGetterService> logger)
        {
            _logger = logger;
        }

        public override Task<Bot> GetBotById(GetBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Get Bot by id Request");

            return Task.FromResult(new Bot
            {
                BotId = 1,
                Title = "BCG BOT"
            }) ;
        }
    }
}
