import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JsonHandlerService {
  private jsonData: any = {
  };
  private apiUrl = 'apiUrl';
  constructor(private http: HttpClient) { }
  getData(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
  generateJsonFile(jsonData: any) {
    return this.http.post('/api/generate-json', jsonData);
  }
  updateJsonData(newData: any) {
    this.jsonData = { ...this.jsonData, ...newData };
  }
}
