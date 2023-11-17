import {Component, TemplateRef, ViewChild} from '@angular/core';
import { ModalDirective } from 'ngx-bootstrap/modal';
import {JsonHandlerService} from "../../service/json-handler.service";

@Component({
  selector: 'app-text-block-page',
  templateUrl: './text-block-page.component.html',
  styleUrls: ['./text-block-page.component.scss']
})
export class TextBlockPageComponent {
  questionFields: {[key: string]: string[]} = {
    "question": [
      "Вопрос",
      "Введите вопрос"
    ],
    "answer_type": [
      "Тип вопроса",
      "Введите тип вопроса"
    ],
    "title": [
      "Название вопроса",
      "Введите название вопроса"
    ]
  }
  @ViewChild(ModalDirective, { static: false }) modal?: ModalDirective;
  modalTitle: string = '';
  modalPlaceHolder: string = '';
  modalValue: string = '';
  currentKey: string = '';
  constructor(private jsonHandlerService: JsonHandlerService) {
    const jsonData = this.jsonHandlerService.getJsonData();
  }
  openModal(key: string) {
    if (this.currentKey == key) {
      if (this.questionFields[key]) {
        this.currentKey = key;
        this.modalTitle = this.questionFields[key][0];
        this.modalPlaceHolder = this.questionFields[key][1];
        this.modal?.show();
      }
    } else {
      if (this.questionFields[key]) {
        this.currentKey = key;
        this.modalTitle = this.questionFields[key][0];
        this.modalPlaceHolder = this.questionFields[key][1];
        this.modalValue = '';
        this.modal?.show();
      }
    }
  }
  saveQuestionField(key: string) {
    this.jsonHandlerService.updateJsonDataModules(key, this.modalValue);
  }
  onModalSubmit() {
    this.saveQuestionField(this.currentKey);
    this.modal?.hide();
  }
  modalHide() {
    this.modal?.hide();
  }
}
