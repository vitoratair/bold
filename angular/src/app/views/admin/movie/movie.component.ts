import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { environment } from '../../../../environments/environment';
import {
	GridColumns,
	GridConfig,
	IGridColumns,
	IGridConfig
} from '../../shared/grid/grid.model';
import { AdminService } from '../admin.service';
import { IMovie, Movie } from './movie.model';

@Component({
	moduleId: module.id,
	selector: 'app-movie',
	templateUrl: 'movie.component.html',
})
export class MovieComponent implements OnInit {
	public headerTitle = 'Movies';
	private url = environment.urls.main + 'api/movie/';
	private urlSync = environment.urls.main + 'api/omdb/sync/';
	public gridConfig: IGridConfig;
	public rows: IMovie[];
	public movie: IMovie = null;
	public show_movie_list = true;
	public show_movie_profile = false;

	constructor(
		private router: Router,
		private movieService: AdminService
	) {}

	ngOnInit() {
		this.configDatatable();
		this.getMovies();
	}

	// GRID
	private configDatatable() {
		this.gridConfig = new GridConfig(this.getColumns());
	}

	private getColumns(): IGridColumns[] {
		const columns: IGridColumns[] = [];

		columns.push(new GridColumns('Title', 'title', null, false, true, 'title'));
		columns.push(new GridColumns('Year', 'year', null, false, true, 'year'));
		columns.push(new GridColumns('Released', 'released', null, false, true, 'released'));
		columns.push(new GridColumns('Rating', 'rating', null, false, true, 'rating'));
		columns.push(new GridColumns('Votes', 'votes', null, false, true, 'votes'));
		columns.push(new GridColumns('Genre', 'genre', null, false, true, 'genre', false));
		columns.push(new GridColumns('Total seasons', 'total_seasons', null, false, true, 'total_seasons', false));

		return columns;
	}

	public rowClick(event: any) {

		if (!event || event === undefined) {
			return;
		}

		this.movie = <IMovie>event['row'];
		this.headerTitle = this.movie.title;
		this.show_movie_list = false;
		this.show_movie_profile = true;
	}

	public goBack() {
		this.movie = null;
		this.show_movie_profile = false;
		this.show_movie_list = true;
	}

	public getMovies() {

		this.movieService
			.getItems(this.url)
			.subscribe((response) => {
				this.rows =  <IMovie[]>response;
			});
	}

	public syncDatabase() {

		  this.movieService
		  .getItems(this.urlSync)
		  .subscribe(() => {
			Swal.fire(
				'Great job!!!',
				'The movies are being sync!!!',
				'success'
			);
		  });
	}

	public showMessageDelete() {
		Swal.fire({
			title: 'Are you sure?',
			text: 'You won\'t be able to revert this!',
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'Yes, delete it!',
		}).then((result) => {
			if (result.isConfirmed) {
				this.cleanDatabase();
			}
		});
	}

	public cleanDatabase() {
		this.movieService
			.deleteItem(this.url)
			.subscribe(() => {
				this.rows = [];
				Swal.fire(
					'Great job!!!',
					'All movies were deleted!!!',
					'success'
				);
			});
	}
}
