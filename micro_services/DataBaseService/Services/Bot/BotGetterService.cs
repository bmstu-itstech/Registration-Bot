using Grpc.Core;
using System.Net;

using DataBaseService.Protos;
using DataBaseService.backend.Types;
using DataBaseService.Backend.Types;

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



            var bot =  MyBot.GetBot(request.BotId, request.Owner);
            

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
            bot_response.StartMessage = bot.start_msg;

            Console.WriteLine(bot_response.TgToken);

            return Task.FromResult(bot_response);
        }

        public override  Task<BotsResponse> GetAllBots(EmptyRequest request, ServerCallContext context)
        {
               _logger.LogInformation("Get Bot by id Request");

            var bots =  MyBot.GetBots();
            bots.Wait();
            var response = new BotsResponse();

            foreach(var bot in bots.Result)
            {
                var bot_response = new BotResponse()
                {
                    State = "OK",
                    Code = 200,
                };

                bot_response.BotSurveyId = bot.bot_survey_id;
                bot_response.GoogleToken = bot.google_token;
                bot_response.TgToken = bot.tg_token;
                bot_response.Owner = bot.owner;
                bot_response.StartMessage = bot.start_msg;

                response.Bots.Add(bot_response);
            }




            return Task.FromResult(response);
        }
        public override Task<Module> GetQuestion(GetQuestionRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Get Bot #{request.BotId}  Question #{request.QuestionId}");

            MyModule question = MyModule.GetMoudleById(request.BotId, request.QuestionId).Result;
         

            return Task.FromResult(MyModule.ConvertToRPC(question));
        }
    }
}
