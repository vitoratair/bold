/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { GridHttpComponent } from './grid-http.component';

describe('GridHttpComponent', () => {
  let component: GridHttpComponent;
  let fixture: ComponentFixture<GridHttpComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GridHttpComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GridHttpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
