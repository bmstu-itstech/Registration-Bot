import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextBlockPageComponent } from './text-block-page.component';

describe('TextBlockPageComponent', () => {
  let component: TextBlockPageComponent;
  let fixture: ComponentFixture<TextBlockPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TextBlockPageComponent]
    });
    fixture = TestBed.createComponent(TextBlockPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
