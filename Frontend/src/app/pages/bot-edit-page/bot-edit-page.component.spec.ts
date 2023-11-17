import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotEditPageComponent } from './bot-edit-page.component';

describe('BotEditPageComponent', () => {
  let component: BotEditPageComponent;
  let fixture: ComponentFixture<BotEditPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BotEditPageComponent]
    });
    fixture = TestBed.createComponent(BotEditPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
