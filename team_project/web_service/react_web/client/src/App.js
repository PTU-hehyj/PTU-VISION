import React from 'react';
import { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState({ members: [] }); // 초기값 수정

  useEffect(() => {
    fetch("/users")
      .then(response => response.json())
      .then(data => setData(data))  // 데이터를 state에 저장
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="App">
      <h1>test 하는 중...</h1>
      <div>
        {/* 삼항연산자 */}
        {data.members.length === 0 ? (
          <p>Loading...</p>
        ) : (
          data.members.map((u, index) => <p key={index}>{u.name}</p>)
        )}
      </div>
    </div>
  );
}

export default App;

// function App() {
//   // state
//   const [data, setData] = useState({ members: [] }); // 초기값값

//   useEffect(() => 
//     {
//     	fetch("/users")
//           .then(
//          // response 객체의 json() 이용하여 json 데이터를 객체로 변화
//           response => response.json())
//           .then(
//           data => {
//             // 받아온 데이터를 data 변수에 update
//             setData(data);
//           }
//         ).catch(
//           (err) => console.log(err)
//         )
//     }, [])

//   return (
//     <div className='App'>
//       <h1>test 하는 중...</h1>
//       <div>
//         {/* 삼항연산자 */}
//         { (typeof data.users === 'undefined') ? (
//           // fetch가 완료되지 않았을 경우에 대한 처리
//           <p>loding...</p>
//         ) : (
//           data.members.map((u) => <p>{u.name}</p>)
//         )}
//       </div>
//     </div>
//   )
// }

// export default App;