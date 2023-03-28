using Google.Protobuf.Collections;
using GoogleSheetsService.Backend;
using Grpc.Core;
using static GoogleSheetsService.SheetReaderService;

namespace GoogleSheetsService.Services
{
    public class ReaderService : SheetReaderServiceBase
    {
        private readonly ILogger<ReaderService> _logger;

        public ReaderService(ILogger<ReaderService> logger)
        {
            _logger = logger;
        }

        public override Task<ReadLineResponse> ReadLine(ReadLineRequest request, ServerCallContext context)
        {
            _logger.LogInformation("ReadLine request");

            var db_controller = new DataBaseController();

            string current_bot_sheet_id = db_controller.Get_bot_sheetId(request.BotId).Result;

            var googleHelper = new GoogleHelper(current_bot_sheet_id);

            List<string> data = new List<string>();
            string state = "Google API error!";
            int code = 1;

            if (googleHelper is not null)
            {
                var sheet_response = googleHelper.ReadTableString(request.ExelId);
                sheet_response.Wait();

                if (!sheet_response.IsFaulted)
                {
                    state = "OK";
                    code = 0;
                    data = sheet_response.Result;
                }
            }

            var response = new ReadLineResponse()
            {
                State = state,
                Code = code,

            };
            response.Data.AddRange(data);
            return Task.FromResult(response);
        }

        public override Task<ReadRangeResponse> ReadRange(ReadRangeRequest request, ServerCallContext context)
        {

            _logger.LogInformation("ReadRange request");

            var db_controller = new DataBaseController();

            string current_bot_sheet_id = db_controller.Get_bot_sheetId(request.BotId).Result;

            var googleHelper = new GoogleHelper(current_bot_sheet_id);


            List<ReadLineResponse> data = new List<ReadLineResponse>();
            string state = "Google API error!";
            int code = 1;

            if (googleHelper is not null)
            {
                var sheets_response = googleHelper.ReadTableRange(request.Range);

                sheets_response.Wait();

                if (!sheets_response.IsFaulted)
                {
                    state = "OK";
                    code = 0;

                    foreach (var list in sheets_response.Result)
                    {
                        var item = new ReadLineResponse()
                        {
                            State = state,
                            Code = code,
                        };
                        item.Data.AddRange(list);
                        data.Add(item);
                    }
                    
                }
            }

            var response = new ReadRangeResponse()
            {
                State = state,
                Code = code,
            };

            response.Data.AddRange(data);

            return Task.FromResult(response);
        }
    }
}
