using DataBaseService.Backend.Config;
using GoogleSheetsService;
using Grpc.Net.Client;
using System.Reflection.PortableExecutable;

namespace DataBaseService.Clients
{
    public class SheetsClient
    {
        public static async Task InputUser(int bot_id,int user_id,List<string> user_data)
        {

        }
        //Создаёт лист "Участники" для нового бота
        public static async Task AddBaseSheet(int bot_id, int user_id, List<string> header)
        {
            using (var channel = GrpcChannel.ForAddress(new ConfigManager().GetSheetApiConnetion()))
            {
                var client = new SheetAppenderService.SheetAppenderServiceClient(channel);

                var append_request = new AppendSheetRequest()
                {
                    BotId = bot_id,
                    FromUser = user_id,
                    Title = "Участники",
                };
                append_request.Header.AddRange(header);

                await client.AppendSheetAsync(append_request);
            }
        }
    }
}
