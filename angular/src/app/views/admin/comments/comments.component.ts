import { IGridConfig, GridConfig, IGridColumns, GridColumns } from './../../shared/grid/grid.model';
import { IComments } from './../movie/movie.model';
import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-comments',
  templateUrl: './comments.component.html',
  styleUrls: ['./comments.component.scss']
})
export class CommentsComponent implements OnInit {

	@Input() comments: IComments[];
	public gridConfig: IGridConfig;

  constructor() { }

  ngOnInit(): void {
	this.configDatatable();
  }

  	// GRID
	private configDatatable() {
		this.gridConfig = new GridConfig(this.getColumns());
	}

	private getColumns(): IGridColumns[] {
		const columns: IGridColumns[] = [];
		columns.push(new GridColumns('Id', 'id', null, false, true, 'id'));
		columns.push(new GridColumns('Comment', 'comment', null, false, true, 'comment'));
		columns.push(new GridColumns('Created', 'created_at', null, false, true, 'created_at'));
		return columns;
	}

}
