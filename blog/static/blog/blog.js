const PostRow = ({ post }) => {
	let thumbnail;
	if (post.hero_image.thumbnail) {
		thumbnail = <img src={post.hero_image.thumbnail} />;
	} else {
		thumbnail = "-";
	}
	return (
		<tr>
			<td>{post.title}</td>
			<td>{thumbnail}</td>
			<td>{post.tags.join(", ")}</td>
			<td>{post.slug}</td>
			<td>{post.summary}</td>
			<td>
				<a href={"/post/" + post.slug}>View</a>
			</td>
		</tr>
	);
};

const PostPagination = (props) => {
	return (
		<nav aria-label="Page navigation example">
			<ul class="pagination">
				<li className={"page-item " + (props.previous ? "" : "disabled")}>
					<button
						class="page-link"
						onClick={(e) => {
							props.changePage(props.previous);
						}}>
						Previous
					</button>
				</li>
				{/* <li class="page-item">
					<a class="page-link" href="#">
						1
					</a>
				</li> */}
				<li className={"page-item " + (props.next ? "" : "disabled")}>
					<button
						class="page-link"
						onClick={(e) => {
							props.changePage(props.next);
						}}>
						Next
					</button>
				</li>
			</ul>
		</nav>
	);
};

const PostTable = ({ dataLoaded, results }) => {
	let rows;
	if (dataLoaded) {
		if (results.length) {
			rows = results.map((post) => <PostRow post={post} key={post.id} />);
		} else {
			rows = (
				<tr>
					<td colSpan="6">No results found.</td>
				</tr>
			);
		}
	} else {
		rows = (
			<tr>
				<td colSpan="6">Loading&hellip;</td>
			</tr>
		);
	}
	return (
		<table
			className="table table-striped table-bordered
        mt-2">
			<thead>
				<tr>
					<th>Title</th>
					<th>Image</th>
					<th>Tags</th>
					<th>Slug</th>
					<th>Summary</th>
					<th>Link</th>
				</tr>
			</thead>
			<tbody>{rows}</tbody>
		</table>
	);
};

class PostTableWrapper extends React.Component {
	state = {
		dataLoaded: false,
		data: null,
	};

	componentDidMount() {
		this.changeUrl(this.props.url);
	}

	changeUrl(url) {
		fetch(url)
			.then((res) => {
				if (res.status !== 200)
					throw new Error(
						"Invalid status from server: " + res.statusText
					);
				return res.json();
			})
			.then((data) => {
				this.setState({
					dataLoaded: true,
					data: data,
				});
			})
			.catch((e) => {
				console.error(e);
				this.setState({
					dataLoaded: true,
					data: { results: [] },
				});
			});
	}

	render() {
		if (this.state.data) {
			const { next, previous, count } = this.state.data;
			return (
				<>
					<PostPagination
						count={count}
						next={next}
						previous={previous}
						changePage={(url) => {
							this.changeUrl(url);
						}}
					/>
					<PostTable
						dataLoaded={this.state.dataLoaded}
						results={this.state.data.results}
					/>
				</>
			);
		}
		return <div>Loading</div>;
	}
}

const domContainer = document.getElementById("react_root");
ReactDOM.render(
	React.createElement(PostTableWrapper, { url: postListUrl }),
	domContainer
);
