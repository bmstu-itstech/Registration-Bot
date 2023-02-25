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
            _logger.LogInformation("Append new Recored request ");
            
            string state = "OK";
            int code = 0;

            return Task.FromResult(new AppendRecordResponse
            {
                Code = code,
                State = state
            });;
        }

        
        public override Task<AppendSheetResponse> AppendSheet(AppendSheetRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Append new Sheet request ");


            string state = "OK";
            int code = 0;

            return Task.FromResult(new AppendSheetResponse
            {
                Code = code,
                State = state
            });
        }
    }
}
