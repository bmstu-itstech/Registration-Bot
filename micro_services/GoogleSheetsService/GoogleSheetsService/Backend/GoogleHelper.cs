using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using GoogleSheetsService.Services;

//TODO
// Нужно где-то запоминать спсок с созданными пользователями листами
// Скорее всего можно заюзать локал базу данных, для микросервиса норм практика

namespace GoogleSheetsService.Backend
{
    public class GoogleHelper
    {
        private static readonly string[] Scopes = { SheetsService.Scope.Spreadsheets };
        private static readonly string ApplicationName = "baumanbot";


        private SheetsService service;
        private GoogleCredential credential;

        private  string SpreadSheetId;


        public GoogleHelper(string table_id)
        {

            this.SpreadSheetId = table_id;
            using (var stream = new FileStream("secretes.json", FileMode.Open, FileAccess.Read))
            {
                this.credential = GoogleCredential.FromStream(stream).CreateScoped(Scopes);

            }

            this.service = new SheetsService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName
            });




        }

        public Task<string> InputObject(object inputObject, string sheet_title)
        {
            //В будущем это будет поле, отвечающее за exel_id новой записи
            string exel_id = "";

            return Task.FromResult<string>(exel_id);
        }

        public Task UpdateObject(string sheet_title, string exel_id, object value)
        {
            return Task.Run(() =>
            {
                // Тут должен быть код, запускающий действие по обновлению записи в новом Task 
            });
        }

        public async Task<BatchUpdateSpreadsheetResponse> AddNewSheet(string sheet_title, ILogger<AppenderService> _logger)
        {
            return await Task.Run(async () =>
            {   
                var body = new BatchUpdateSpreadsheetRequest()
                {
                    Requests = new List<Request>()
                    {
                        new Request()
                        {
                            AddSheet = new AddSheetRequest()
                            {
                                Properties = new SheetProperties()
                                {
                                    Title = sheet_title,

                                }
                            }
                        }
                    }
                };

                 var request = service.Spreadsheets.BatchUpdate(body, this.SpreadSheetId);

              
                 return await request.ExecuteAsync();

            });

        }

        public Task<object> ReadTableString(string sheet_title, string exel_id)
        {
            object get_object = null;

            return Task.FromResult(get_object);
        }

        public Task<List<object>> ReadTableRange(string sheet_title, string exel_id, string range)
        {
            List<object> get_objects = new List<object>();

            return Task.FromResult(get_objects);
        }

    }
}
