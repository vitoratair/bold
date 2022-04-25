import {
	IGridConfig,
	IGridHttpColumns,
	IGridHttpConfig,
	IGridMenusColumns,
} from './../grid/grid.model';
import { environment } from './../../../../environments/environment';
import { AdminService } from './../../admin/admin.service';
import { HttpClient } from '@angular/common/http';
import {
	Component,
	Input,
	Output,
	ViewChild,
	OnInit,
	AfterViewInit,
	EventEmitter,
	ChangeDetectorRef,
	OnChanges,
} from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { merge, Observable, of as observableOf } from 'rxjs';
import { catchError, map, startWith, switchMap } from 'rxjs/operators';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';

@Component({
	selector: 'app-grid-http',
	templateUrl: './grid-http.component.html',
	styleUrls: ['./grid-http.component.scss'],
})
export class GridHttpComponent implements OnInit, AfterViewInit {
	@Input() gridConfig: IGridHttpConfig;
	@Input() refreshDatatable: boolean = false;
	@Output() rowClick = new EventEmitter();

	public no_filter = true;
	public dataSource;
	public selection;
	displayedColumns: string[] = [];
	exampleDatabase: HttpDatabase | null;
	data: ResultApi[] = [];

	resultsLength = 0;
	isLoadingResults = true;
	isRateLimitReached = false;

	@ViewChild(MatPaginator) paginator: MatPaginator;
	@ViewChild(MatSort) sort: MatSort;

	constructor(
		private _service: AdminService,
		private _httpClient: HttpClient,
		private changeDetectorRefs: ChangeDetectorRef
	) {}

	ngOnInit() {
		this.displayedColumns = this.gridConfig.columns.map(function (item) {
			return item.data;
		});
		this.selection = new SelectionModel<any>(true, []);
	}

	rowEmit() {
		this.rowClick.emit(this.selection.selected);
	}

	ngAfterViewInit(search: string = null) {
		this.no_filter = search === null;

		this.exampleDatabase = new HttpDatabase(
			this.gridConfig.href,
			this._service,
			this._httpClient
		);
		this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
		console.log(this.paginator);
		merge(this.sort.sortChange, this.paginator.page)
			.pipe(
				startWith({}),
				switchMap(() => {
					this.isLoadingResults = true;
					return this.exampleDatabase.fetchData(
						this.sort.active,
						this.sort.direction,
						this.paginator.pageIndex,
						this.paginator.pageSize,
						search
					);
				}),
				map((data) => {
					this.isLoadingResults = false;
					this.isRateLimitReached = false;
					this.resultsLength = data.count;
					return data.results;
				}),
				catchError(() => {
					this.isLoadingResults = false;
					this.isRateLimitReached = true;
					return observableOf([]);
				})
			)
			.subscribe((data) => {
				this.dataSource = new MatTableDataSource(data);
				this.data = data;
				this.changeDetectorRefs.detectChanges();
			});
	}

	public onSelect(selected: any) {
		this.rowClick.emit(selected);
	}

	public applyFilter(event: any) {
		if (!event.isTrusted) return false;
		if (event.key !== 'Enter') return false;

		const filterValue: string = (event.target as HTMLInputElement).value
			.trim()
			.toLowerCase();
		let filter = [];

		// CHECK AND OPERATOR
		filter = filterValue.split(' && ');
		let finalFilter = [];
		this.gridConfig.filter_by.forEach((item) => {
			finalFilter.push(`&${item}=${filter.join('|')}`);
		});

		this.ngAfterViewInit(finalFilter.join(''));
	}

	public menuEventClick(id: string, row: any) {
		this.rowClick.emit({ id: id, row: row });
	}

	isColumnVisible(name: string) {
		return this.displayedColumns.findIndex((col) => col === name) > 0;
	}

	/** Whether the number of selected elements matches the total number of rows. */
	isAllSelected() {
		if (this.dataSource === undefined) {
			return false;
		}
		const numSelected = this.selection.selected.length;
		const numRows = this.dataSource.data.length;
		return numSelected === numRows;
	}

	/** Selects all rows if they are not all selected; otherwise clear selection. */
	masterToggle() {
		if (this.dataSource === undefined) {
			return false;
		}
		this.isAllSelected()
			? this.selection.clear()
			: this.dataSource.data.forEach((row) => this.selection.select(row));
	}

	/** The label for the checkbox on the passed row */
	checkboxLabel(row?: any): string {
		if (!row) {
			return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
		}
		return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${
			row.position + 1
		}`;
	}

	columnClick(name: string) {
		const colIndex = this.displayedColumns.findIndex((col) => col === name);

		if (colIndex > 0) {
			// column is currently shown in the table, so we remove it
			this.displayedColumns.splice(colIndex, 1);
		} else {
			// column is not in the table, so we add it
			this.displayedColumns.push(name);
		}
	}

	public showMenuItem(menu: IGridMenusColumns, row: any) {
		if (menu.is_visible) {
			return true;
		}

		if (row === undefined) {
			return false;
		}

		const visibility_data = row[menu.visibility_data];
		const expected_result = menu.visibility_data_return;

		return visibility_data === expected_result;
	}
}

export interface ResultApi {
	results: any[];
	count: number;
}

/** An example database that the data source uses to retrieve data for the table. */
export class HttpDatabase {
	private token = 'Token ' + localStorage.getItem('auth_token');

	constructor(
		private href: string,
		private service: AdminService,
		private _httpClient: HttpClient
	) {}

	fetchData(
		sort: string,
		order: string,
		page: number,
		page_size: number,
		search: string = null
	): Observable<ResultApi> {
		const ordering = `${
			this.href.indexOf('?') === -1 ? '?' : '&'
		}ordering=${order === 'desc' ? '-' : ''}${sort}`;
		const headers = {
			'Content-Type': 'application/json',
			Authorization: this.token,
		};
		let requestUrl = `${this.href}${ordering}&page_size=${page_size}&page=${
			page + 1
		}${search ? search : ''}`;
		return this._httpClient.get<ResultApi>(requestUrl, { headers });
	}
}
