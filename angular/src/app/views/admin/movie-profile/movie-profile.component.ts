import { IMovie, IEpisode, IComments } from './../movie/movie.model';
import { Component, OnInit, Input } from '@angular/core';
import { environment } from '../../../../environments/environment';
import {
	GridColumns,
	GridConfig,
	GridMenusColumns,
	IGridColumns,
	IGridConfig,
	IGridMenusColumns,
} from '../../shared/grid/grid.model';
import { AdminService } from '../admin.service';

@Component({
  selector: 'app-movie-profile',
  templateUrl: './movie-profile.component.html',
  styleUrls: ['./movie-profile.component.scss']
})
export class MovieProfileComponent implements OnInit {
	@Input() movie: IMovie;
	private url = environment.urls.main;
	public data: IMovie | IEpisode;
	public rows: IEpisode[];
	public comments: IComments[];
	public gridConfig: IGridConfig;
	public title = 'Episodes';
	public show_comments = false;

	constructor(
		private movieService: AdminService
	) {
		this.configDatatable();
  	}

  ngOnInit(): void {
	  this.data = <IMovie>this.movie;
	  this.rows = this.movie.episodes;
	  this.url = environment.urls.main + 'api/comment/?episode=';
  }

	// GRID
	private configDatatable() {
		this.gridConfig = new GridConfig(this.getColumns());
	}

	private getColumns(): IGridColumns[] {
		const columns: IGridColumns[] = [];
		columns.push(new GridColumns('Title', 'title', null, false, true, 'title'));
		columns.push(new GridColumns('Season', 'season', null, false, true, 'season'));
		columns.push(new GridColumns('Episode number', 'episode_number', null, false, true, 'episode_number'));
		columns.push(new GridColumns('Rating', 'rating', null, false, true, 'rating'));
		columns.push(new GridColumns('Votes', 'votes', null, false, true, 'votes'));

		return columns;
	}

	private showComments() {
		this.title = 'Comments';
		this.show_comments = true;
		const url = this.url + this.data.id;

		this.movieService
		.getItems(url)
		.subscribe((response) => {
			this.comments =  <IComments[]>response;
		});

	}


	public rowClick(event) {
		if (!event || event === undefined) {
			return;
		}

		const data: IEpisode = event['row'];
		this.data = data;
		this.showComments();
		window.scroll(0, 0);
	}

}
