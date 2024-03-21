import { Link } from "react-router-dom";

const Missing = () => {
  return (
    <section className="loginPage_sec">
      <div className="container">
        <h3>Route Not Found</h3>
        <Link to={"/"}>Go Back to Home</Link>
      </div>
    </section>
  );
};

export default Missing;
