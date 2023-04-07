using Grpc.Core;
using System.Net;

using DataBaseService.Protos;
using DataBaseService.backend.Types;

namespace DataBaseService.Services.bot
{
    public class BotGetterService : BotGetter.BotGetterBase
    {
        private readonly ILogger<BotGetterService> _logger;

        public BotGetterService(ILogger<BotGetterService> logger)
        {
            _logger = logger;
        }

        public override Task<BotResponse> GetBot(GetBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Get Bot by id Request");



            var bot = MyBot.GetBot(request.BotId, request.Owner).Result;
            var bot_response = new BotResponse()
            {
                State = "OK",
                Code = 200,
            };


            if (bot == null)
            {
                bot_response.State = "Error while getting bot";
                bot_response.Code = 401;

                return Task.FromResult(bot_response);
            }

            bot_response.BotSurveyId = bot.bot_survey_id;
            bot_response.GoogleToken = bot.google_token;
            bot_response.TgToken = bot.tg_token;
            bot_response.Owner = bot.owner;

            return Task.FromResult(bot_response);
        }
    }
}
