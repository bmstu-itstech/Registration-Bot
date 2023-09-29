import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class JsonHandlerService {
  currentQuestionNumber = 1;
  private jsonData: any = {
    "journal": {
      "modules": {
      }
    }
  };
  private apiUrl = 'apiUrl';
  constructor(private http: HttpClient) { }
  getJsonData() {
    return this.jsonData;
  }
  generateJsonFile(jsonData: any) {
    return this.http.post('/api/generate-json', jsonData);
  }
  updateJsonData(newData: any) {
    this.jsonData = { ...this.jsonData, ...newData };
    console.log(this.getJsonData());
  }
  updateJsonDataModules(newData: any) {
    this.jsonData.journal.modules = { ...this.jsonData.journal.modules, ...newData };
    console.log(this.getJsonData());
  }
}
