export interface IComments {
	id: number;
	comment: string;
}

export class Comments implements IComments {
	constructor (
		public id: number,
		public comment: string,
	) {}
}

export interface IMovie {
	id: number;
	title: string;
	total_seasons: number;
	year: string;
	released: string;
	genre: string;
	rating: number;
	votes: number;
	actors: string;
	poster_url: string;
	plot: string;
	awards: string;
	episodes: Episode[];
}

export class Movie implements IMovie {
	constructor (
		public id: number,
		public title: string,
		public total_seasons: number,
		public year: string,
		public released: string,
		public genre: string,
		public rating: number,
		public votes: number,
		public actors: string,
		public poster_url: string,
		public plot: string,
		public awards: string,
		public episodes: Episode[],
	) {}
}

export interface IEpisode {
	id: number;
	title: string;
	year: string;
	released: string;
	genre: string;
	rating: number;
	votes: number;
	actors: string;
	poster_url: string;
	plot: string;
	awards: string;
}

export class Episode implements IEpisode {
	constructor (
		public id: number,
		public title: string,
		public year: string,
		public released: string,
		public genre: string,
		public rating: number,
		public votes: number,
		public actors: string,
		public poster_url: string,
		public plot: string,
		public awards: string,
	) {}
}
