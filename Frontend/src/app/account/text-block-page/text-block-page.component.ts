import {Component, ViewChild} from '@angular/core';
import {BsModalRef} from "ngx-bootstrap/modal";
import {JsonHandlerService} from "../../service/json-handler.service";

interface Question {
  question: string;
  answer_type: string;
  title: string;
  buttons: any[];
  next_id: number | null;
}

@Component({
  selector: 'app-text-block-page',
  templateUrl: './text-block-page.component.html',
  styleUrls: ['./text-block-page.component.scss']
})
export class TextBlockPageComponent {
  @ViewChild('lgModal1') lgModal1!: BsModalRef;
  @ViewChild('lgModal2') lgModal2!: BsModalRef;
  question: string = '';
  telegramToken: string = '';
  constructor(private jsonHandlerService: JsonHandlerService) {
    const jsonData = this.jsonHandlerService.getJsonData();
  }
  saveQuestion() {
    const currentQuestionNumber = this.jsonHandlerService.getCurrentQuestionNumber();
    const newQuestionKey = currentQuestionNumber.toString();
    const jsonData = this.jsonHandlerService.getJsonData() as { journal: { modules: Record<string, Question> } };
    const lastQuestion: Question | undefined = Object.values(jsonData.journal.modules).pop();
    if (lastQuestion) {
      lastQuestion.question = this.question;
    }
    this.jsonHandlerService.updateJsonDataModules(jsonData);
    const updatedQuestionNumber = currentQuestionNumber + 1;
    this.jsonHandlerService.saveCurrentQuestionNumber(updatedQuestionNumber);
  }
  saveTgToken() {
    const newData = {
      "tg_token": this.telegramToken,
    }
    this.jsonHandlerService.updateJsonData(newData);
  }
  onQuestionSubmit() {
    this.saveQuestion()
    this.question = '';
    this.lgModal1.hide();
  }
  onTelegramTokenSubmit() {
    this.saveTgToken()
    this.telegramToken = '';
    this.lgModal2.hide();
  }

}
