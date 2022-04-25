import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Import Containers
import { DefaultLayoutComponent } from './containers';

import { P404Component } from './views/error/404.component';


export const routes: Routes = [
	{
		path: '',
		redirectTo: 'admin',
		pathMatch: 'full',
	},
	{
		path: 'admin',
		component: DefaultLayoutComponent,
		data: {
			title: 'Admin',
		},
		children: [
			{
				path: '',
				loadChildren: () =>
					import('./views/admin/admin.module').then(
						(m) => m.AdminModule
					),
			},
		],
	},
	{ path: '**', component: P404Component },
];

@NgModule({
	imports: [
		RouterModule.forRoot(routes, {
			onSameUrlNavigation: 'reload',
		}),
	],
	exports: [RouterModule],
})
export class AppRoutingModule {}
