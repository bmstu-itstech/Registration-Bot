import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class JsonHandlerService {
  private currentQuestionNumberKey = 'currentQuestionNumber';
  private apiUrl = 'http://localhost:3000/';
  constructor(private http: HttpClient) {}
  getCurrentQuestionNumber() {
    const storedValue = localStorage.getItem(this.currentQuestionNumberKey);
    return storedValue ? parseInt(storedValue, 10) : 1;
  }
  saveCurrentQuestionNumber(currentQuestionNumber: number) {
    localStorage.setItem(this.currentQuestionNumberKey, currentQuestionNumber.toString());
  }
  getJsonData() {
    const jsonData = localStorage.getItem('jsonData');
    return jsonData ? JSON.parse(jsonData) : null;
  }
  saveJsonData(data: any) {
    localStorage.setItem('jsonData', JSON.stringify(data));
  }
  parseJsonFile(jsonData: any) {
    return this.http.post(this.apiUrl + 'parse-json', jsonData);
  }
  updateJsonData(newData: any) {
    const jsonData = this.getJsonData();
    const updatedData = { ...jsonData, ...newData };
    this.saveJsonData(updatedData);
    console.log(updatedData);
  }
  updateJsonDataModules(newData: any) {
    const jsonData = this.getJsonData();
    if (!jsonData.journal) {
      jsonData.journal = {};
    }
    if (!jsonData.journal.modules) {
      jsonData.journal.modules = {};
    }
    const updatedModules = { ...jsonData.journal.modules, ...newData };
    const updatedData = { ...jsonData, journal: { modules: updatedModules } };
    this.saveJsonData(updatedData);
    console.log(updatedData);
  }
}
