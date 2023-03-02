using Google.Apis.Sheets.v4.Data;
using GoogleSheetsService.Backend;
using Grpc.Core;
using static Google.Apis.Requests.BatchRequest;

namespace GoogleSheetsService.Services
{
    public class AppenderService : SheetAppenderService.SheetAppenderServiceBase
    {
        private readonly ILogger<AppenderService> _logger;

        public AppenderService(ILogger<AppenderService> logger)
        {
            _logger = logger;
        }


        public override Task<AppendRecordResponse> AppendRecord(AppendRecordRequest request, ServerCallContext context)
        {
            GoogleHelper googleHelper = new GoogleHelper(request.TableId); ;


            _logger.LogInformation("Append new Recored request ");

            string state = "Google API error!";
            int code = 1;

            if (googleHelper != null)
            {
                state = "OK";
                code = 0;
            }


            return Task.FromResult(new AppendRecordResponse
            {
                Code = code,
                State = state
            }); ;
        }


        public override Task<AppendSheetResponse> AppendSheet(AppendSheetRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Append new Sheet request ");

            GoogleHelper googleHelper = new GoogleHelper(request.TableId); ;


            string state = "Google API error!\n";
            int code = 1;

            if (googleHelper != null)
            {
                try
                {
                    var response = googleHelper.AddNewSheet(request.Title, _logger);
                    response.Wait();

                    if(!response.IsFaulted)
                    {
                        state = "OK";
                        code = 0;
                    }
                }
                catch (Exception ex)
                {

                    _logger.LogInformation("Erorr has ocured in AddNewSheet Requests!");
                    state += ex.Message;

                }

            }

            return Task.FromResult(new AppendSheetResponse
            {
                Code = code,
                State = state
            });
        }
    }
}
