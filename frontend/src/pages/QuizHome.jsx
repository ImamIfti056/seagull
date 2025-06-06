import Category from "../components/Quiz/Category";
import { Helmet } from "react-helmet-async";

const QuizHome = () => {
	return (
		<>
			<Helmet>
				<title>Quiz | KUETx</title>
			</Helmet>
			<div className="text-center">
				<div className="container mx-auto py-8 px-4">
					<h1 className="text-3xl font-bold text-center mb-8">
						KUETx <span className="text-blue-600">Quizzes</span>
					</h1>
					<p className="text-lg text-center">
						Test your skills with KUETxs&apos; Quizzes.
					</p>
				</div>
				<Category />
			</div>
		</>
	);
};

export default QuizHome;
