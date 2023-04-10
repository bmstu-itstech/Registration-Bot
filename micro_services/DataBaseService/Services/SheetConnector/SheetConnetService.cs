using DataBaseService.backend.Types;
using DataBaseService.Protos;
using Grpc.Core;

namespace DataBaseService.Services.SheetConnector
{
    public class SheetConnetService : Protos.SheetConnector.SheetConnectorBase
    {
        public override  Task<GoogleToken> GetGoogleSheetsToken(GetGoogleSheetsTokenRequest request, ServerCallContext context)
        {

            string token = MyBot.GetBot(request.BotId, request.Owner).Result.google_token;

            return Task.FromResult(new GoogleToken() { Token = token });
        }
    }
}
