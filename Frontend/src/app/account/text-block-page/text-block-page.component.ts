import {Component, TemplateRef, ViewChild} from '@angular/core';
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
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
  @ViewChild('lgModal') lgModal!: BsModalRef;
  modalTitle: string = '';
  modalPlaceHolder: string = '';
  modalValue: string = '';
  constructor(private jsonHandlerService: JsonHandlerService, private modalService: BsModalService) {
    const jsonData = this.jsonHandlerService.getJsonData();
  }
  openModal(key: string, template: TemplateRef<any>) {
    if (this.questionFields[key]) {
      this.modalTitle = this.questionFields[key][0];
      this.modalPlaceHolder = this.questionFields[key][1];
      this.modalValue = '';
      this.lgModal = this.modalService.show(template);
    }
  }
  onModalSubmit() {
    this.lgModal.hide();
  }
}
