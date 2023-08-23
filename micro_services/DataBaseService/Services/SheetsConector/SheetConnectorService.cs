using DataBaseService.backend.Types;
using DataBaseService.Protos;
using DataBaseService.Services.bot;
using Grpc.Core;

namespace DataBaseService.Services.SheetsConector
{
    public class SheetConnectorService : SheetConnector.SheetConnectorBase
    {
        private readonly ILogger<SheetConnectorService> _logger;

        public SheetConnectorService(ILogger<SheetConnectorService> logger)
        {
            _logger = logger;
        }


        public override Task<GoogleToken> GetGoogleSheetsToken(GetGoogleSheetsTokenRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Get Bot {request.BotId} Sheets Token");

            var google_token = new GoogleToken()
            {
                Token = MyBot.GetBot(request.BotId, request.Owner).Result.google_token
            };


            return Task.FromResult(google_token);
        }
    }
}
