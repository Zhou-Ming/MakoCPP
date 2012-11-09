<%!
from makocpp.CPP import primitive
%>

<%def name="if_guard(header_name, cbody, cppbody)" filter='trim'>
<%
    guard_def = '__' + header_name.replace('/', '_').upper() + '_H__'
%>
#ifndef ${guard_def}
#define ${guard_def}
${ifdef('__cplusplus', ['extern "C" {'])}
% for i in cbody:
${i}
% endfor
<%
    cppbody_ = ['}'] + cppbody
%>
${ifdef('__cplusplus', cppbody_)}
#endif // ${guard_def}
</%def>

<%def name="header(header_name, cbody, cppbody)" filter='trim'>
${if_guard(header_name, cbody, cppbody)}
</%def>
