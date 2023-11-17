import {Component, OnInit} from '@angular/core';
import {JsonHandlerService} from "../../service/json-handler.service";
import {GraphComponent} from "../../graph/graph.component";

@Component({
  selector: 'app-creation-page',
  templateUrl: './creation-page.component.html',
  styleUrls: ['./creation-page.component.scss']
})
export class CreationPageComponent {
  clearLocalStorage(){
    return localStorage.clear();
  }
  constructor(private jsonHandlerService: JsonHandlerService) {
    const jsonData = this.jsonHandlerService.getJsonData();
  }
  isSectionVisible = true;
  addJsonQuestion() {
    const currentQuestionNumber = this.jsonHandlerService.getCurrentQuestionNumber()
    const newQuestionKey = (currentQuestionNumber).toString();
    const newData = {
      [newQuestionKey]: {
        "question": "",
        "answer_type": "",
        "title": "",
        "buttons": [],
        "next_id": null
      }
    }
    this.jsonHandlerService.updateJsonDataJournal(newData);
    const updatedQuestionNumber = currentQuestionNumber + 1;
    this.jsonHandlerService.saveCurrentQuestionNumber(updatedQuestionNumber);
    this.isSectionVisible = !this.isSectionVisible;
  }
}
