import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SendingPageComponent } from './sending-page.component';

describe('SendingPageComponent', () => {
  let component: SendingPageComponent;
  let fixture: ComponentFixture<SendingPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SendingPageComponent]
    });
    fixture = TestBed.createComponent(SendingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
