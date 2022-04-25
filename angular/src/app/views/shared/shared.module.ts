
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GridComponent } from './grid/grid.component';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';

import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatListModule } from '@angular/material/list';
import { NgSelectModule } from '@ng-select/ng-select';


@NgModule({
	imports: [
		CommonModule,
		MatIconModule,
		MatMenuModule,
		MatTableModule,
		MatPaginatorModule,
		MatSortModule,
		MatButtonModule,
		MatCardModule,
		MatFormFieldModule,
		MatInputModule,
		MatCheckboxModule,
		MatSelectModule,
		MatProgressSpinnerModule,
		MatListModule,
		NgSelectModule
	],
	exports: [
		GridComponent,
		MatMenuModule,
		MatTableModule,
		MatIconModule,
		MatPaginatorModule,
		MatSortModule,
		MatButtonModule,
		MatCardModule,
		MatFormFieldModule,
		MatInputModule,
		MatCheckboxModule,
		MatSelectModule,
		MatProgressSpinnerModule,
		MatListModule,
		NgSelectModule
	],
	declarations: [
		GridComponent
	],
	providers: [
	],
})
export class SharedModule {}
