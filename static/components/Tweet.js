export default class Tweet extends React.Component {
    render() {
        return (
            <div className="row">
            <from>
                <div>
                    <textarea ref="tweetTextArea"/>
                    <label>How do you doing?</label>
                    <button>Tweet now</button>
                </div>
            </from>
        </div >
        );
    }
}