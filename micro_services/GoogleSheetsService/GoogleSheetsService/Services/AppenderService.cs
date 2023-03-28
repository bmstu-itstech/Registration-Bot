using Google.Apis.Sheets.v4.Data;
using Google.Protobuf.WellKnownTypes;
using GoogleSheetsService.Backend;

using Grpc.Core;

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
            _logger.LogInformation("Append new Recored request");


            var db_controller = new DataBaseController();

            string current_bot_sheet_id = db_controller.Get_bot_sheetId(request.BotId).Result;

            var googleHelper = new GoogleHelper(current_bot_sheet_id);


            string state = "Google API error!";
            int code = 1;
            string exel_id = "";

            if (googleHelper != null)
            {
                try
                {

                    var response = googleHelper.InputObject(request.Data.ToList(), request.SheetTitle, this._logger);
                    response.Wait();

                    if (!response.IsFaulted)
                    {
                        state = "OK";
                        code = 0;
                        exel_id = response.Result;
                    }

                }
                catch (Exception ex)
                {
                    _logger.LogInformation("Erorr has ocured in Append new Recored request!");
                    state += ex.Message;
                }
            }


            return Task.FromResult(new AppendRecordResponse
            {
                Code = code,
                State = state,
                ExelId = exel_id,

            }); ;
        }

        public override Task<AppendSheetResponse> AppendSheet(AppendSheetRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Append new Sheet request ");

            var db_controller = new DataBaseController();

            string current_bot_sheet_id = db_controller.Get_bot_sheetId(request.BotId).Result;

            var googleHelper = new GoogleHelper(current_bot_sheet_id);


            string state = "Google API error!\n";
            int code = 1;

            if (googleHelper != null)
            {
                try
                {

                    var response = googleHelper.AddNewSheet(request.Title, request.Header.ToList(), _logger);
                    response.Wait();

                    if (!response.IsFaulted)
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

        public override Task<UpdateRecordResponse> UpdateRecord(UpdateRecordRequest request, ServerCallContext context)
        {
            _logger.LogInformation($"Update Record at {request.ExelId}");

            var db_controller = new DataBaseController();

            string current_bot_sheet_id = db_controller.Get_bot_sheetId(request.BotId).Result;

            var googleHelper = new GoogleHelper(current_bot_sheet_id);

            string state = "Google API error!\n";
            int code = 1;

            if (googleHelper != null)
            {
                try
                {
                    var task_response = googleHelper.UpdateObject(request.NewData.ToList(), request.ExelId);
                    task_response.Wait();


                    if (!task_response.IsFaulted)
                    {
                        state = "OK";
                        code = 0;
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogInformation("Erorr has ocured in UpdateRecord Requests!");
                    state += ex.Message;
                }
            }

            return Task.FromResult(new UpdateRecordResponse
            {
                State = state,
                Code = code,
            }); ;
        }
    }
}
