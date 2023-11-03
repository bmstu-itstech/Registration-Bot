import {Component, OnInit} from '@angular/core';
import {JsonHandlerService} from "../../service/json-handler.service";
import {GraphComponent} from "../../graph/graph.component";
import {MatDialog, MatDialogConfig} from "@angular/material/dialog";
import {TextBlockPageComponent} from "../../account/text-block-page/text-block-page.component";

@Component({
  selector: 'app-creation-page',
  templateUrl: './creation-page.component.html',
  styleUrls: ['./creation-page.component.scss']
})
export class CreationPageComponent {
  constructor(private jsonHandlerService: JsonHandlerService, private dialog: MatDialog) {
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
    this.jsonHandlerService.updateJsonDataModules(newData);
    const updatedQuestionNumber = currentQuestionNumber + 1;
    this.jsonHandlerService.saveCurrentQuestionNumber(updatedQuestionNumber);
    this.isSectionVisible = !this.isSectionVisible;
  }

  protected readonly GraphComponent = GraphComponent;
  protected readonly open = open;

  openModal() {
    const dialogRef = this.dialog.open(TextBlockPageComponent, {
      maxWidth: '100vw',
      maxHeight: '100vh',
      height: 'calc(100vh - 188px)',
      width: '100%',
      panelClass: 'full-screen-modal',
      position: {top: '188px'},
      disableClose: true
    });
  }
}
