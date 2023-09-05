using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using GoogleSheetsService.Services;
using System.Diagnostics.SymbolStore;

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
            using (var stream = new FileStream("secrets.json", FileMode.Open, FileAccess.Read))
            {
                this.credential = GoogleCredential.FromStream(stream).CreateScoped(Scopes);

            }

            this.service = new SheetsService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName
            });

        }

        public async Task<string> InputObject(List<string> data, string sheet_title, ILogger<AppenderService> _logger)
        {
            return await Task.Run(async () =>
            {

                string range = $"{sheet_title}!A:Z";

                var obj_list = new List<object>();

                foreach (var el in data)
                {
                    obj_list.Add(el);
                }

                var valueRange = new ValueRange();
                valueRange.Values = new List<IList<object>>() { obj_list };


                var add_header_request = service.Spreadsheets.Values.Append(valueRange, this.SpreadSheetId, range);
                add_header_request.ValueInputOption = SpreadsheetsResource.ValuesResource.AppendRequest.ValueInputOptionEnum.USERENTERED;

                var response = await add_header_request.ExecuteAsync();

                string exel_id = response.TableRange;


                string sheet = exel_id.Split('!')[0];
                string response_range = exel_id.Split('!')[1];

                string first_loc = response_range.Split(':')[0];
                string second_loc_char = response_range.Split(':')[1][0].ToString();
                int second_loc_pos = Int32.Parse(response_range.Split(':')[1].Remove(0, 1)) +1;

                string output_exel_id = $"{sheet}!{first_loc}:{second_loc_char}{second_loc_pos}";

                return output_exel_id;

            });
        }

        public Task UpdateObject(List<string> data, string exel_id)
        {
            return Task.Run(async () =>
            {
                string range = $"{exel_id}";

                var obj_list = new List<object>();

                foreach (var el in data)
                {
                    obj_list.Add(el);
                }

                var valueRange = new ValueRange();
                valueRange.Values = new List<IList<object>>() { obj_list };


                var updateRequest = service.Spreadsheets.Values.Update(valueRange, this.SpreadSheetId, range);
                updateRequest.ValueInputOption = SpreadsheetsResource.ValuesResource.UpdateRequest.ValueInputOptionEnum.USERENTERED;

                var response = await updateRequest.ExecuteAsync();

            });
        }

        public async Task<BatchUpdateSpreadsheetResponse> AddNewSheet(string sheet_title,List<string> header, ILogger<AppenderService> _logger)
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

                var response = await request.ExecuteAsync();


                string range = $"{sheet_title}!A:Z";
                
                var obj_list = new List<object>();

                foreach (var el in header)
                {
                    obj_list.Add(el);
                }

                var valueRange = new ValueRange();
                valueRange.Values = new List<IList<object>>() { obj_list };

           
                var add_header_request = service.Spreadsheets.Values.Append(valueRange, this.SpreadSheetId, range);
                add_header_request.ValueInputOption = SpreadsheetsResource.ValuesResource.AppendRequest.ValueInputOptionEnum.USERENTERED;

                add_header_request.Execute();


                 return response;
            });

        }

        public Task<List<string>> ReadTableString(string exel_id)
        {
            return Task.Run(() => 
            {
                // Понял, что метод чтения строки идентичен чтению диапазона, но из 1 строки
                // однако, логически более правильно разделить это на 2 метода
                // потому что в будущем нужно будет, например, считать строку соотвествующему конкретному пользователю

                return ReadTableRange(exel_id).Result[0];
            });
        }

        public Task<List<List<string>>> ReadTableRange( string range)
        {
            return Task.Run(async () =>
            {

                var request = service.Spreadsheets.Values.Get(this.SpreadSheetId, range);

                var response = await request.ExecuteAsync();

                List<List<string>> values = new List<List<string>>();

                if (response.Values?.Count > 0)
                {
                    foreach(var row in response.Values)
                    {
                        List<string> curr_row = new List<string>();

                        foreach(var elem in row)
                        {
                            curr_row.Add(elem.ToString());
                        }

                        values.Add(curr_row);
                    }
                }


                return values;
            });
        }

    }
}
