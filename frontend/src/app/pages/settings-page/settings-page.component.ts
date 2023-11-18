import {Component, ViewChild} from '@angular/core';
import {BsModalRef} from "ngx-bootstrap/modal";
import {JsonHandlerService} from "../../service/json-handler.service";

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.scss']
})
export class SettingsPageComponent {
  @ViewChild('lgModal1') lgModal1!: BsModalRef;
  @ViewChild('lgModal2') lgModal2!: BsModalRef;
  apiToken: string = '';
  telegramToken: string = '';
  constructor(private jsonHandlerService: JsonHandlerService) {
    const jsonData = this.jsonHandlerService.getJsonData();
  }
  saveApiToken() {
    const newData = {
      "sheets_token": this.apiToken
    }
    this.jsonHandlerService.updateJsonData(newData);
  }
  saveTgToken() {
    const newData = {
      "tg_token": this.telegramToken,
    }
    this.jsonHandlerService.updateJsonData(newData);
  }
  onApiTokenSubmit() {
    this.saveApiToken()
    this.apiToken = '';
    this.lgModal1.hide();
  }
  onTelegramTokenSubmit() {
    this.saveTgToken()
    this.telegramToken = '';
    this.lgModal2.hide();
  }
}
