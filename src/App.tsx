import { Routes, Route, Outlet } from "react-router-dom";
import SchemaBuilder from "./pages/SchemaBuilder";
import Missing from "./components/router/Missing"
import Home from "./pages/Home";

function App() {

  const Layout = () => {
    return (
      <div className="flex">
        <div className="flex flex-col min-w-0 w-[100%]">
          hello
          <Outlet />
        </div>
      </div>
    );
  };

  return (
      <Routes>
        <Route element={<Layout />} >
          <Route path="/" element={<Home />} />
          <Route path="/schema/create" element={<SchemaBuilder />} />
          <Route path="*" element={<Missing />} />
        </Route>
      </Routes >
  );
}

export default App;
