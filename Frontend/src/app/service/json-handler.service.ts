import { Injectable } from '@angular/core';
import {Edge, Layout, Node} from "@swimlane/ngx-graph";
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class JsonHandlerService {
  private currentQuestionNumberKey = 'currentQuestionNumber';
  private apiUrl = 'http://localhost:12000';
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
  getGraphDataFromModules() {
    const jsonData = this.getJsonData();
    const graphData: any = {nodes: [], links: []};
    if (jsonData && jsonData.journal && jsonData.journal.modules) {
      for (const moduleKey of Object.keys(jsonData.journal.modules)) {
        const module = jsonData.journal.modules[moduleKey];
        const newQuestionKey = moduleKey;
        const node: Node = {
          id: newQuestionKey,
          label: module.title
        };
        graphData.nodes.push(node);
        if (module.next_id) {
          const edge: Edge = {
            source: newQuestionKey,
            target: module.next_id,
            label: ''
          };
          graphData.links.push(edge);
        }
      }
    }
    return graphData;
  }
  saveJsonData(data: any) {
    localStorage.setItem('jsonData', JSON.stringify(data));
  }
  parseJsonFile(jsonData: any) {
    return this.http.post(this.apiUrl + '/parse-json', jsonData);
  }
  updateJsonData(newData: any) {
    const jsonData = this.getJsonData();
    const updatedData = { ...jsonData, ...newData };
    this.saveJsonData(updatedData);
    console.log(updatedData);
  }
  updateJsonDataJournal(newData: any) {
    const jsonData = this.getJsonData() || {};
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
  updateJsonDataModules(fieldName: string, newValue: any) {
    const jsonData = this.getJsonData();
    if (!jsonData.journal) {
      jsonData.journal = {};
    }
    if (!jsonData.journal.modules) {
      jsonData.journal.modules = {};
    }
    const moduleKeys = Object.keys(jsonData.journal.modules);
    const lastModuleKey = moduleKeys.length > 0 ? moduleKeys[moduleKeys.length - 1] : null;
    if (lastModuleKey) {
      if (jsonData.journal.modules[lastModuleKey][fieldName] !== undefined) {
        jsonData.journal.modules[lastModuleKey][fieldName] = newValue;
        this.saveJsonData(jsonData);
        console.log(jsonData);
      }
    }
  }
}
