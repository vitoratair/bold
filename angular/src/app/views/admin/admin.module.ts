// Angular Imports
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TruncateModule } from 'ng2-truncate';

// This Module's Components
import { AdminRoutingModule } from './admin-routing.module';
import { AdminService } from './admin.service';
import { SharedModule } from '../shared/shared.module';
import { DataFilterPipe } from './data-filter-pipe';

import { MovieComponent } from './movie/movie.component';
import { MovieProfileComponent } from './movie-profile/movie-profile.component';
import { CommentsComponent } from './comments/comments.component';

@NgModule({
	imports: [
		CommonModule,
		FormsModule,
		ReactiveFormsModule,
		AdminRoutingModule,
		TruncateModule,
		SharedModule,
	],
	declarations: [
		DataFilterPipe,
		// CATEGORY //
		MovieComponent,
		MovieProfileComponent,
		CommentsComponent,
	],
	exports: [],
	providers: [AdminService],
})
export class AdminModule {}
