import {Component, ViewChild} from '@angular/core';
import {BsModalRef} from "ngx-bootstrap/modal";

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
  onApiTokenSubmit() {
    this.apiToken = '';
    this.lgModal1.hide();
  }
  onTelegramTokenSubmit() {
    this.telegramToken = '';
    this.lgModal2.hide();
  }
}
